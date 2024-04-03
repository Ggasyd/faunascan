import React from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider, Outlet , useLocation } from "react-router-dom";
import HomePage from "./Routes/HomePage";
import Reports from "./Routes/Reports";

// Importez d'autres composants pour les routes ici

const AppLayout = () => (
  <>
    
    <Outlet />
  </>
);

const router = createBrowserRouter([
  {

  
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <HomePage/>,
      },
      {
        path: "/home",
        element: <HomePage />,
      },
      {
        path: "reports",
        element: <Reports />,
      },
    
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);
