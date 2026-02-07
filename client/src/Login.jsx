export default function Login() {
    return (
        <>
            <div className="w-full h-full flex justify-center items-center bg-(--secondary-color)">
                <div className="flex flex-col justify-start items-center w-3/4 md:w-1/2 lg:w-1/2 xl:w-1/2 2xl:w-1/2 h-auto">
                    <div className="font-bold text-(--text-primary-color) p-2">
                        Login to Gmail Account
                    </div>

                    <div className="w-full p-2">
                        <div className="text-(--text-primary-color) text-[10px]">Email Address</div>
                        <input type="text" className="bg-white w-full mt-1 text-[15px] p-1" />
                    </div>

                    <div className="w-full p-2">
                        <div className="text-(--text-primary-color) text-[10px]">Password</div>
                        <input type="password" className="bg-white w-full mt-1 text-[15px] p-1" />
                    </div>

                    <div className="w-full p-2 flex flex-row justify-end items-center">
                        <button className="border border-white bg-white pt-1 pb-1 pl-3 pr-3 rounded text-[10px] hover:cursor-pointer">
                            Login
                        </button>
                    </div>
                </div>
            </div>
        </>
    )
}