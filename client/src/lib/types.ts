export interface ContentWithText {
    quillData : Content;
    text : string;
}

export interface Userdata {
    username : string;
    password : string;
    description? : string;
}

export interface Content {
    title : string;
    content : {
        ops : NestedInterface[]
    };
    tags : string[];
}

export interface ContentTitle {
    title : string;
    username : string;
    tags : string[];
    self_url : string
}

export interface ContentScreenData {
    content : Content;
    related_blogs : ContentTitle[]
}

export interface Profile {
    username : string;
    description : string;
    joined_at : string;
    blogs : ContentTitle[]
}

interface NestedInterface {
    [key : string] : string | NestedInterface | boolean | number;
}