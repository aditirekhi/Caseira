import { HttpContext, HttpContextToken } from '@angular/common/http';

export const SHOULD_CHECK_TOKEN_EXPIRATION = new HttpContextToken<boolean>(() => true);

export const withTokenExpirationCheck = (enabled: boolean): HttpContext =>
    new HttpContext().set(SHOULD_CHECK_TOKEN_EXPIRATION, enabled);
