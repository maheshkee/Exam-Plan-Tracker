import Navbar from "./Navbar";

export default function PageLayout({ children }) {
  return (
    <div>
      <Navbar />
      <div style={{
        maxWidth: 900,
        margin: "0 auto",
        padding: "24px 16px",
      }}>
        {children}
      </div>
    </div>
  );
}
