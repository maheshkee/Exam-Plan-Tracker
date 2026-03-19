const variants = {
  primary: {
    background: "var(--primary)",
    color: "white",
  },
  success: {
    background: "var(--success)",
    color: "white",
  },
  danger: {
    background: "var(--danger)",
    color: "white",
  },
  secondary: {
    background: "var(--gray-200)",
    color: "var(--gray-700)",
  },
};

export default function Button({
  children,
  variant = "primary",
  onClick,
  type = "button",
  fullWidth = false,
  style = {},
  disabled = false,
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        ...variants[variant],
        padding: "10px 20px",
        border: "none",
        borderRadius: 6,
        cursor: disabled ? "not-allowed" : "pointer",
        fontSize: 14,
        fontWeight: 600,
        width: fullWidth ? "100%" : "auto",
        opacity: disabled ? 0.6 : 1,
        ...style,
      }}
    >
      {children}
    </button>
  );
}
