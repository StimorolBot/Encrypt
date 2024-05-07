import Cookies from "universal-cookie";

const cookies = new Cookies();
cookies.sameSite = "none";
cookies.partitioned = true;
cookies.httpOnly = true;

export default cookies;