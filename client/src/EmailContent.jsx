import DropdownIcon from "./assets/dropdown-icon.png";
import { Tooltip } from 'react-tooltip';

export default function EmailContent({ email }) {
    return (
        <>
            <div className="w-full h-full pr-5 pl-5 flex justify-center items-center overflow-hidden">
                <div className="w-full h-full flex flex-col justify-start items-start">

                    {/* Title for Email */}
                    <div className="w-full h-auto text-2xl bg-purple-50">
                        {email[0]["subject"]}
                    </div>

                    {/* Metadata about the email */}
                    <div className="w-full flex justify-start items-start pt-3">
                        <div className="text-xs grow">

                            {/* Sender Username */}
                            <div className="font-bold">
                                {(email[0]["sender"]).split("<", 1)[0]}
                            </div>

                            {/* Additional Details */}
                            <div className="flex justify-start items-end">
                                <div>to me</div>
                                <img
                                    src={DropdownIcon}
                                    className="w-[20px] hover:cursor-help"
                                    data-tooltip-id="email-info"
                                ></img>

                                {/* Tooltip showing more details on hover */}
                                <Tooltip
                                    id="email-info"
                                    place="bottom"
                                    style={{ backgroundColor: "var(--secondary-color)" }}
                                >
                                    <div>from: {email[0]["sender"]} </div>
                                    <div>to: {email[0]["receiver"]} </div>
                                    <div>cc: {email[0]["cc"] ? email[0]["cc"]: "-"}</div>
                                </Tooltip>
                            </div>
                        </div>

                        {/* Date and time of Email sent */}
                        <div className="text-xs"> {email[0]["date"]} </div>
                    </div>

                    <div className="mt-3 mb-2 p-3 text-sm font-light w-full h-full bg-(--primary-color) overscroll-contain overflow-scroll scrollbar-hide">
                        {email[0]["body"]["preferred"] == "text/html" ?
                            // <div
                            //     className="email-body"
                            //     dangerouslySetInnerHTML={{ __html: email[0]["body"]["html"] }}
                            // />
                            <iframe
                                sandbox=""
                                className="w-full h-full border-0 bg-white"
                                srcDoc={email[0]["body"]["html"]}
                            />
                            :
                            email[0]["body"]["text"]}
                    </div>
                </div>
            </div>
        </>
    )
}