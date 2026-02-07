export default function EmailList({ emails, setSelectedEmailId }) {

    const selectEmail = (emailID) => {
        setSelectedEmailId(emailID);
    }

    return (
        <div
            id="Email_List_Container"
            className="w-full grow overscroll-contain overflow-scroll scrollbar-hide"
        >
            <div className="p-1 w-full h-[70px]">
                {emails.map((email, index) => {
                    return (
                        <div key={index} onClick= {() => selectEmail(email.id)} className="bg-(--primary-color) w-full h-full flex justify-start items-center p-1 hover:cursor-pointer">
                            <div className="text-xs w-[40%] truncate font-semibold">
                                {email.subject}
                            </div>
                            <div className="text-xs w-[60%] truncate">
                                {email["body"]["text"]}
                            </div>
                        </div>
                    )
                })}
            </div>

        </div>
    );
}
