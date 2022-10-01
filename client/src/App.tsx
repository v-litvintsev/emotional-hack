import { Routes, Route } from "react-router-dom";
import { Auth } from "./views/Auth";
import { Home } from "./views/Home";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/auth" element={<Auth />} />
    </Routes>
  );
};

export default App;
