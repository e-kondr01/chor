export interface IErrorData {
  response: {
    data: {
      non_field_errors: string[];
      errors: {
        field: string;
        code: string;
      }[];
    };
  };
}
