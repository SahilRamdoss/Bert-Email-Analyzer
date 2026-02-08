import User_Icon from "./assets/User_Icon.png";
import EmailList from "./EmailList.jsx";
import EmailContent from "./EmailContent.jsx";
import NoEmailContent from "./NoEmailContent.jsx";
import { useEffect, useState } from "react";
import serverAPI from "./api/server.jsx";
import DOMPurify from "dompurify";
import "./Home.css";

export default function Home() {

    const [emails, setEmails] = useState([]);
    const [selectedEmailId, setSelectedEmailId] = useState('');
    const [loading, setLoading] = useState(true);

    const fetchEmails = (async () => {
        try {
            console.log("Loading...");
            setLoading(true);
            const response = await serverAPI.get("/");

            if (response.status == 200) {
                console.log(response);
                const data = response["data"];

                data.forEach(email => {
                    if (email["body"]["preferred"] == "text/html") {
                        email["body"]["html"] = DOMPurify.sanitize(email["body"]["html"], { USE_PROFILES: { html: true }, FORBID_ATTR: ["opacity", "filter"] })
                    }
                });

                setEmails(data);
            } else {
                console.warn("Could not fetch the emails from backend");
            }

            setLoading(false);
            console.log("Done!");
        } catch (e) {
            console.warn(`An exception occured when fetching the emails: ${e}`);
        }
    })

    useEffect(() => {
        fetchEmails();
    }, [])

    useEffect(() => {
        console.log("Selected email Id changed to ", selectedEmailId)
    }, [selectedEmailId])

    return (
        <>
            <div className="relative w-full h-full bg-(--tertiary-color) p-2 flex flex-col justify-start items-center">
                {/* This is the top banner*/}
                <div className="bg-(--secondary-color) w-full h-12 flex justify-end items-center">
                    <div className="text-white font-bold">
                        {emails.length > 0 ?
                            emails[0]["user"]
                            :
                            "User"
                        }
                    </div>
                    <div className="ps-2 pe-2">
                        <img src={User_Icon} />
                    </div>
                </div>

                {loading ?
                    <div className="loader">
                        <div className="loader-subcontainer">
                            <div className="spinner">
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                            </div>
                            <div className="text-white mt-3">Loading...</div>
                        </div>
                    </div>
                    :
                    <div></div>
                }

                <div className="w-full h-full flex flex-row justify-start items-center">
                    <div className="w-[30%] h-full flex flex-col justify-start items-center">
                        {/*Container for the pull email button */}
                        <div className="p-2 w-full h-(--pullemailsblock-height) flex flex-row justify-end items-center">
                            <button type="button" onClick={() => fetchEmails()} className="text-[10px] pt-0.5 pb-0.5 ps-2 pe-2 font-bold border-2 border-(--primary-color) bg-(--primary-color) rounded-md hover:cursor-pointer">
                                Pull Emails
                            </button>
                        </div>

                        {/* List of emails in chronological order */}
                        {emails.length > 0 ?
                            <EmailList emails={emails} setSelectedEmailId={setSelectedEmailId} /> :
                            <div></div>
                        }

                    </div>
                    <div className="w-[70%] h-full flex flex-col justify-start items-center">
                        {/* Empty container to fill in space */}
                        <div className="p-2 w-full h-(--pullemailsblock-height)">
                            {/* Empty */}
                        </div>

                        {/* Email Viewer */}

                        {selectedEmailId != '' ?
                            <EmailContent email={emails.filter((e) => e.id == selectedEmailId)} /> :
                            <NoEmailContent />
                        }
                    </div>
                </div>
            </div>
        </>
    )
}