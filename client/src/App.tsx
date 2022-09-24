import { Routes, Route } from "react-router-dom";
import { Home } from "./views/Home";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
    </Routes>
  );
};

export default App;
