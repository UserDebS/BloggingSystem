import { add, Search, leftArrow, user } from "@/svgs/Svgs";
import { Input } from "./input";
import { Button } from "./button";
import { useContext } from "react";
import { appContext } from "./Layout";
import { checkSession } from "@/lib/sessionManager";

const Header = () => {
    const { navigateTo } = useContext(appContext);
    return (
        <div className="header w-full h-16 flex justify-between shadow-md">
            <div className="logo h-full min-w-[151.65px] max-w-[25%] flex justify-start pl-5 grow">
                <img className="h-full min-w-0" src="logo.png" alt="logo" />
            </div>
            <div className="nav-container flex gap-2 items-center justify-end h-full min-w-[169px] max-w-[75%] grow px-2">
                {
                    checkSession()? 
                    <>
                        {window.location.pathname !== '/compose' ? <>
                        <div className="search-field h-12 w-auto bg-slate-100 rounded-[10px] flex px-2 focus-within:border focus-within:border-slate-600 relative">
                            {Search}
                            <Input
                                className="border-none shadow-none h-full text-[18px] font-medium placeholder:text-[18px] placeholder:font-medium"
                                placeholder="Search"
                                onChange={e => console.log(e.currentTarget.value)}
                            />
                            <div className="suggestions absolute w-full h-auto"></div>
                        </div>
                        <Button
                            onClick={_ => navigateTo('/compose')}
                            className="bg-slate-700 text-slate-100 font-bold h-12 hover:bg-slate-600 rounded-[10px]"
                        >{add}&nbsp; New Post</Button>
                        </> : ''}
                        <div className="avatar rounded-[40%] h-12 w-12 bg-slate-800 cursor-pointer text-white p-2">
                            {user}
                        </div>
                    </> : 
                        <Button
                        onClick={_ => window.location.pathname !== '/auth'? navigateTo('/auth') : navigateTo('/')}
                        className="bg-slate-700 text-slate-100 font-bold h-12 hover:bg-slate-600 rounded-[10px] px-4 text-[17px]"
                        >{window.location.pathname !== '/auth'? 'Log In' : <>{ leftArrow }&nbsp; Go back</>}
                        </Button>
                }
            </div>
        </div>
    )
}

export default Header;