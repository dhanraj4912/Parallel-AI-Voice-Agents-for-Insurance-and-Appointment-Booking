import { BrowserRouter, Routes, Route } from "react-router-dom";

import App from "./App";
import Dashboard from "./components/Dashboard";
import Assistant from "./components/Assistant";
import Recommendation from "./components/Recommendation";
import Success from "./components/Success";

import UserContext from "./context/UserContext";

function Root() {
  return (
    <BrowserRouter>
      <UserContext>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/assistant" element={<Assistant />} />
          <Route path="/recommendation" element={<Recommendation />} />
          <Route path="/success" element={<Success />} />
        </Routes>
      </UserContext>
    </BrowserRouter>
  );
}

export default Root;