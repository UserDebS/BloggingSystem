import { ContentScreenData, ContentTitle, ContentWithText, Profile, Userdata } from "./types";

function requestHandler() {
    const baseRoute : string = 'http://127.0.0.1:5500/';
    return {
        verifyToken : async function() : Promise<number> {
            return await fetch(baseRoute, {
                method : 'GET',
                credentials : 'include',
            }).then(_ => 200).catch(_ => 404);
        }, 
        signUp : async function(userdata : Userdata) {
            return await fetch(baseRoute + 'signup', {
                method : 'POST',
                credentials : 'include',
                body : JSON.stringify(userdata)
            }).then(_ => 201).catch(_ => 409);
        },
        login : async function(userdata : Userdata) {
            return await fetch(baseRoute + 'login', {
                method : 'POST',
                credentials : 'include',
                body : JSON.stringify(userdata)
            }).then(_ => 200).catch(_ => 404);
        },
        blogs : async function(offset : number) : Promise<ContentTitle[]>{
            return await fetch(baseRoute + `blogs/?offset=${offset}`, {
                method : 'GET',
                credentials : 'include',
            }).then(res => res.json())
            .catch(_ => []);
        },
        channel : async function(username : string, offset : number) : Promise<Profile> {
            return await fetch(baseRoute + `?username=${username}&offset=${offset}`, {
                method : 'GET',
                credentials : 'include'
            }).then(res => res.json())
            .catch(_ => []);
        },
        blogById : async function(blogId : number, offset : number) : Promise<ContentScreenData | null> {
            return await fetch(baseRoute + `blogs/${blogId}/?offset=${offset}`, {
                method : 'GET',
                credentials : 'include'
            }).then(res => res.json())
            .catch(_ => null);
        },
        blogBySearch : async function(search : string, offset : number) : Promise<ContentTitle[]> {
            return await fetch(baseRoute + `blogs/?search=${search}&offset=${offset}`).then(res => res.json())
            .catch(_ => []);
        },
        upload : async function(contentWithText : ContentWithText) : Promise<any>{
            return await fetch(baseRoute + `upload`, {
                method : 'POST',
                credentials : 'include',
                body : JSON.stringify(contentWithText)
            }).then(res => res.json())
            .catch(_ => {
                return {
                    status : 409
                };
            })
        }
    }
}

export const requester = requestHandler();