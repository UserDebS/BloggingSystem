import { useRef, useState } from "react";
import {
    Card,
    CardTitle,
    CardHeader,
    CardFooter,
    CardContent
} from '@/components/ui/card';
import { Button } from "@/components/ui/button";
import { Userdata } from "@/lib/types";

const Auth = () => {
    const [logIn, setLogIn] = useState(true);
    return (
        <div className="auth-screen h-full">
            <div className="h-full w-full flex justify-center items-center">
                <Card>
                    <CardHeader>
                        <CardTitle className="capitalize text-xl">{logIn? 'Sign In to your account' : 'Create your account'}</CardTitle>
                    </CardHeader>
                    {logIn? <CardContent>
                        <p>Card Content</p>
                    </CardContent> : 
                    <CardContent>

                    </CardContent>
                    }
                    <CardFooter>
                        <Button></Button>
                    </CardFooter>
                </Card>

            </div>
        </div>
    );
}

export default Auth;