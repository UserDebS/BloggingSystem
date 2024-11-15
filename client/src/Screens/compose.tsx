import Editor from "@/components/ui/Editor";

const Compose = () => {
    return ( 
        <div className="blog-compose h-full">
            <Editor readOnly={false} fetchedContent={null} />
        </div>
    );
}
 
export default Compose;