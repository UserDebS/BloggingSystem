import { checkSession, createSession } from "@/lib/sessionManager";
import { useEffect, createContext, useCallback } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import Header from "./Header";

type AppContextType = {
    navigateTo: (desiredPath: Readonly<string>) => void
}

export const appContext = createContext<AppContextType>({
    navigateTo: () => { }
})

const Layout = () => {
    const navigate = useNavigate();
    const navigateTo = useCallback((desiredPath: Readonly<string>) => {
        const path: Readonly<string> = desiredPath.match(/^\/[a-z]*/g)?.[0] as string;
        const pathModule: Readonly<{ [key: string]: boolean }> = {
            '/': false,
            '/auth': false,
            '/home': true,
            '/compose': true
        };
        if (path === "undefined" || pathModule[path] === undefined) { return; }
        const res: boolean = checkSession();
        if (res && pathModule[path]) {
            navigate(desiredPath);
        } else if (res) navigate('/home');
        else if(pathModule[path]) navigate('/auth');
        else navigate(desiredPath);
    }, [])
    useEffect(() => {
        const desiredPath: Readonly<string> = window.location.pathname;
        const path: Readonly<string> = desiredPath.match(/^\/[a-z]*/g)?.[0] as string;
        const pathModule: Readonly<{ [key: string]: boolean }> = {
            '/': false,
            '/auth': false,
            '/home': true,
            '/compose': true
        };
        if (path === "undefined" || pathModule[path] === undefined) { return; }
        if (!checkSession()) {
            createSession().then(res => {
                if (res && pathModule[path]) {
                    return;
                } else if (res) navigate('/home');
                else if (pathModule[path]) navigate('/');
            })
        }
    }, []);
    return (
        <appContext.Provider value={{navigateTo}}>
            <div className="h-lvh overflow-hidden">
                <Header />
                <main className="h-[calc(100lvh-4rem)] w-full overflow-y-auto">
                    <Outlet />
                </main>
            </div>
        </appContext.Provider>
    );
}

export default Layout;