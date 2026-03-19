export default function Card({ children, style = {} }) {
  return (
    <div style={{
      background: "var(--white)",
      borderRadius: 8,
      padding: 24,
      marginBottom: 20,
      boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
      ...style,
    }}>
      {children}
    </div>
  );
}
