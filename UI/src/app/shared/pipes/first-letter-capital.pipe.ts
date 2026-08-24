import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'firstLetterCapital',
})
export class FirstLetterCapitalPipe implements PipeTransform {

  transform(value: unknown, ...args: unknown[]): string | undefined {
    if (typeof value === 'string' && value.length > 0) {
      return value.charAt(0).toUpperCase() + value.slice(1);
    }
    return undefined;
  }

}
