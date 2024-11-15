import { requester } from "./requestHandler";

export const checkSession = () : boolean => {
    if(window.sessionStorage.getItem('blog_session')) return true;
    return false;
}   

export const createSession = async() : Promise<boolean> => {
    try {
        const status : number = await requester.verifyToken();
        if(status === 200) window.sessionStorage.setItem('blog_session', 'active')
        return status === 200;
    } catch(e : any) {
        return false;
    }
}