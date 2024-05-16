export interface IErrorData {
    non_field_errors: string[],
    errors: 
      {
        field: string,
        code: string
      }[]
}