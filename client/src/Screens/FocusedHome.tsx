import { useParams } from "react-router-dom";

const FocusedHome = () => {
    const { blogId } = useParams();
    return ( 
        <div className="h-full">
            {blogId}
        </div>
    );
}
 
export default FocusedHome;