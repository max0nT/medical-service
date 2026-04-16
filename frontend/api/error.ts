const FIELD_LABELS: Record<string, string> = {
  first_name: "Имя",
  last_name: "Фамилия",
  email: "Email",
  password: "Пароль",
  password_repeat: "Повтор пароля",
  sync_with_google_calendar: "Синхронизация с Google Calendar",
  id: "ID",
  start: "Дата начала",
  end: "Дата окончания",
};

function toText(value: unknown): string | null {
  if (typeof value === "string") {
    const trimmed = value.trim();
    return trimmed.length > 0 ? trimmed : null;
  }

  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }

  return null;
}

function localizeField(loc: unknown): string | null {
  if (!Array.isArray(loc) || loc.length === 0) {
    return null;
  }

  const parts = loc
    .map((part) => toText(part))
    .filter((part): part is string => Boolean(part))
    .filter((part) => part !== "body" && part !== "query" && part !== "path");

  if (parts.length === 0) {
    return null;
  }

  const field = parts[parts.length - 1];
  if (!field) {
    return null;
  }

  return FIELD_LABELS[field] ?? field;
}

function localizeMessage(msg: unknown, type: unknown): string | null {
  const text = toText(msg);
  const messageType = toText(type) ?? "";

  if (!text) {
    if (messageType === "missing") {
      return "поле обязательно";
    }
    return null;
  }

  const lower = text.toLowerCase();

  if (lower === "field required") {
    return "поле обязательно";
  }

  if (lower.includes("valid email")) {
    return "некорректный email";
  }

  if (lower.includes("should be a valid boolean")) {
    return "должно быть значением true или false";
  }

  if (lower.includes("should be a valid string")) {
    return "должно быть строкой";
  }

  if (lower.includes("should be a valid integer")) {
    return "должно быть целым числом";
  }

  if (lower.includes("string should have at least")) {
    return "слишком короткое значение";
  }

  if (lower.includes("string should have at most")) {
    return "слишком длинное значение";
  }

  return text;
}

function parseDetail(detail: unknown): string | null {
  const text = toText(detail);
  if (text) {
    return text;
  }

  if (Array.isArray(detail)) {
    const messages = Array.from(
      new Set(
        detail
      .map((item) => parseDetail(item))
      .filter((item): item is string => Boolean(item)),
      ),
    );

    return messages.length > 0 ? messages.join("\n") : null;
  }

  if (detail && typeof detail === "object") {
    const value = detail as Record<string, unknown>;
    const nested = parseDetail(value.detail);
    if (nested) {
      return nested;
    }

    const msg =
      localizeMessage(value.msg, value.type) ??
      localizeMessage(value.message, value.type) ??
      localizeMessage(value.error, value.type);
    const loc = localizeField(value.loc);

    if (msg && loc) {
      return `${loc}: ${msg}`;
    }

    if (msg) {
      return msg;
    }
  }

  return null;
}

export function extractApiErrorMessage(
  responseBody: unknown,
  fallback = "Не удалось выполнить запрос",
): string {
  return parseDetail(responseBody) ?? fallback;
}
