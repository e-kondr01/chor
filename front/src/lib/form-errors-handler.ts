import { FormInstance } from 'antd';
import { IErrorData } from '../api/config/api-schema';
import { SetStateAction } from 'react';

function isFieldError(error: unknown): error is IErrorData {
    return typeof error === 'object' && error != null && 'errors' in error
}

export const formErrorsHandler = <T>(form: FormInstance<T>, e: unknown, setFormError: React.Dispatch<SetStateAction<string>>) => {
        if (isFieldError(e)) {
            form.setFields(
                e?.errors?.map(({ field, code }) => ({
                    name: field,
                    errors: [code],
                })),
            );
            if (!e.errors.length && !!e.non_field_errors.length) {
                setFormError(e.non_field_errors[0])
            }
        }
};
