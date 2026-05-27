export const medicalTheme = {
  colors: {
    background: "#F3FAF8",
    surface: "#FFFFFF",
    surfaceMuted: "#E9F5F2",
    primary: "#1F8A70",
    primaryDark: "#176A57",
    secondary: "#3EB7A0",
    accent: "#D8F3EC",
    text: "#12312B",
    textMuted: "#5F7F77",
    border: "#CFE7E0",
    danger: "#C85C5C",
    warningBg: "#FFF4E0",
    warningText: "#8F5A1C",
  },
  shadow: {
    shadowColor: "#0A3C32",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.08,
    shadowRadius: 18,
    elevation: 4,
  },
  radius: {
    sm: 12,
    md: 18,
    lg: 28,
    pill: 999,
  },
};

export function buildAvatarUri(avatar: string | null | undefined, apiUrl?: string): string | null {
  if (!avatar) {
    return null;
  }

  if (avatar.startsWith("http://") || avatar.startsWith("https://")) {
    return avatar;
  }

  if (!apiUrl) {
    return avatar;
  }

  const normalizedBase = apiUrl.endsWith("/") ? apiUrl.slice(0, -1) : apiUrl;
  const normalizedPath = avatar.startsWith("/") ? avatar : `/${avatar}`;

  return `${normalizedBase}${normalizedPath}`;
}

export function getDisplayName(firstName?: string | null, lastName?: string | null): string {
  const fullName = [firstName, lastName]
    .map((value) => (value ?? "").trim())
    .filter(Boolean)
    .join(" ");

  return fullName || "Пациент клиники";
}
