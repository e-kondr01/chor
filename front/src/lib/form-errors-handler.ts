import { FormInstance } from "antd";
import { IErrorData } from "../api/config/api-schema";
import { SetStateAction } from "react";

function isFieldError(error: unknown): error is IErrorData {
  return typeof error === "object" && error != null && "response" in error;
}

export const formErrorsHandler = <T>(
  form: FormInstance<T>,
  e: unknown,
  setFormError: React.Dispatch<SetStateAction<string>>
) => {
  if (isFieldError(e)) {
    const error = e?.response?.data;
    form.setFields(
      error?.errors?.map(({ field, code }) => ({
        name: field,
        errors: [code],
      }))
    );
    if (!error?.errors.length && !!error?.non_field_errors.length) {
      setFormError(error?.non_field_errors[0]);
    }
  } else {
    setFormError("Непредвиденная ошибка. Попробуйте позже.");
  }
};
