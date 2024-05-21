import { useEffect, useRef } from "react";

import "./timer.sass";


export const Timer = ({ date, seconds, setSeconds, setIsShown, delay }) => {
    const circleRef = useRef();
    const secondsString = String(seconds % 60).padStart(2, "0");
    
    if (circleRef?.current){
        const radius =  circleRef?.current?.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        circleRef.current.style.strokeDasharray = `${circumference} ${circumference}`;
        circleRef.current.style.strokeDashoffset = 0;
        const offset =  circumference - seconds / delay * circumference;
        circleRef.current.style.strokeDashoffset = offset;
    }
        
    useEffect(() => {
        const timer = setInterval(() => {
            setSeconds((state) => Math.max(state-1, 0));
        }, 1000);
        
        return () => {
            clearInterval(timer);
            setSeconds(delay);
        }
    }, [date]);

    if (seconds === 0)
        setIsShown((s) => !s);

    return(
        <div className="timer__container">       
        <svg className="timer-svg"  width="40" height="40">
            <circle className="timer" cx="50%" cy="50%" r="15" ref={circleRef} />
            <circle className="timer-bg" cx="50%" cy="50%" r="15"/>
            <text className="timer-text" x="11" y="26">{ secondsString }</text>
        </svg>
        
        </div>
    );
}
