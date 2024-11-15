import { Button } from "@/components/ui/button";
import { appContext } from "@/components/ui/Layout";
import { useContext } from "react";

const Landing = () => {
    const {navigateTo} = useContext(appContext);
    return (
        <div className="landing h-full">
            <div className="w-full h-full flex relative flex-wrap">
                <div className="h-2/3 w-[40%] min-w-[442.1px] absolute bg-white shadow-md rounded-r-[100px] z-10 top-1/2 translate-y-[-50%] pl-24 pr-5 py-24">
                    <h1 className="uppercase font-extrabold text-5xl"><strong className="text-[#cb6ce6]">BLOG</strong> YOUR <br /> IDEAS</h1>
                    <br />
                    <p className="text-slate-400 text-2xl">Got ideas, but having hard time to reach your audience? Try BlogIt and reach your audience faster ;)</p>
                    <br />
                    <Button onClick={_ => navigateTo('/auth')} className="bg-slate-700 text-white text-xl rounded-xl py-6 hover:bg-slate-600">Get Started</Button>
                </div>
                <div className="h-full w-1/3 z-0">
                </div>
                <div className="image-container h-full w-2/3 bg-black z-0">
                    <img src="background.jpg" alt="background" className="h-full w-full object-cover"/>
                </div>
            </div>
        </div>
    );
}

export default Landing;