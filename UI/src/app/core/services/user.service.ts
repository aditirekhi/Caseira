import { inject, Service } from '@angular/core';
import { AuthenticationResponse, UserSignInRequest } from '../../shared/interfaces/authentication.interface';
import { HttpClient } from '@angular/common/http';
import { ApiResponse } from '../../shared/interfaces/generic.interface';
import { Observable, map } from 'rxjs';
import { RouteConstants } from '../../shared/components/constants/route-constants';

@Service()
export class UserService {

}
