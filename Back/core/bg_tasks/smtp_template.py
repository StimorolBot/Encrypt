from typing import TYPE_CHECKING
from core.operations.operation import generate_code

if TYPE_CHECKING:
    from pydantic import EmailStr
    from email.message import EmailMessage


def email_confirm(email: "EmailMessage", location: str, user_email: "EmailStr", user_agent: str) -> list:
    code_confirm = generate_code()
    email["Subject"] = "Подтверждение почты"

    email.set_content(f"""
        <div style="color: #e3e7e9;">
            <div class="email__container" style="margin-top: 20px; font-size: 20px; border-radius: 10px;
                max-width: 800px; background-color: hsl(223, 10%, 25%); max-height: 600px;">
                
                <div class="wrapper" style="padding: 30px; display: block; overflow: hidden;">
                    <h2 class="email-username" style="text-align: center; overflow: hidden"> 
                        Здравствуй 
                    </h2>
                    
                    <div class="email__code-container" style="overflow: hidden;">
                        <p class="email-code-msg" style="color: #fff; cursor: auto; text-decoration: none;> 
                            Код, необходимый для регистрации {user_email}
                        </p>
                        <p class="email-code" style="color: #1e96ff; font-weight: 800; font-size: 60px; text-align: center;
                            background-color: #2a2a2d; padding: 15px; border-radius: 5px;"> {code_confirm} </p>
                    </div>
                    
                    <div class="email__info-container" style="overflow: hidden;">
                        <p class="email-info">
                            Вы получили это письмо из-за попытки регистрации учетной записи
                            из браузера {user_agent} по адресу {location}
                        </p>
                        <p class="email-info" style="padding-top: 20px; overflow: hidden;">
                            Если вы не пытались создать учетную запись, проигнорируйте это письмо
                        </p>
                    </div>
                </div>
            </div>
        </div> """, subtype="html")

    return [email, code_confirm]


def reset_password(email: "EmailMessage", location: str, user_email: "EmailStr", user_agent: str) -> list:
    code_confirm = generate_code()
    email["Subject"] = "Сброс Пароля"

    email.set_content(f"""
        <div style="color: #e3e7e9;">
            <div class="email__container" style="margin-top: 20px; font-size: 20px; border-radius: 10px;
                max-width: 800px; background-color: hsl(223, 10%, 25%); max-height: 600px;">

                <div class="wrapper" style="padding: 30px; display: block; overflow: hidden;">
                    <h2 class="email-username" style="text-align: center; overflow: hidden"> 
                        Здравствуй 
                    </h2>

                    <div class="email__code-container" style="overflow: hidden;">
                        <p class="email-code-msg" style="color: #fff; cursor: auto; text-decoration: none;> 
                            Код, необходимый для регистрации {user_email}
                        </p>
                        <p class="email-code" style="color: #1e96ff; font-weight: 800; font-size: 60px; text-align: center;
                            background-color: #2a2a2d; padding: 15px; border-radius: 5px;"> {code_confirm} </p>
                    </div>

                    <div class="email__info-container" style="overflow: hidden;">
                        <p class="email-info">
                            Вы получили это письмо из-за попытки регистрации учетной записи
                             из браузера {user_agent} по адресу {location}
                        </p>
                        <p class="email-info" style="padding-top: 20px; overflow: hidden;">
                            Если вы не пытались создать учетную запись, проигнорируйте это письмо
                        </p>
                    </div>
                </div>
            </div>
        </div> """, subtype="html")

    return [email, code_confirm]
