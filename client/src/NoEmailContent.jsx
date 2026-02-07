import NoContent from "./assets/no_content.png";

export default function NoEmailContent() {
    return (
        <>
            <div className="w-full h-full p-5 flex justify-center items-center">
                <div className="w-full h-full bg-(--secondary-color) flex justify-center items-center">
                    <img src={NoContent} />
                </div>
            </div>
        </>
    )
}