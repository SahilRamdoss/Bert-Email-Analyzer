import { useState, useEffect, lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

const Home = lazy(() => import("./Home.jsx"));
const Login = lazy(() => import("./Login.jsx"));
const Error404 = lazy(() => import("./Error404.jsx"));

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="*" element={<Error404 />} />
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App
