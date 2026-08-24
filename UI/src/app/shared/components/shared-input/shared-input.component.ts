import { Component, forwardRef, input, output } from '@angular/core';
import { ControlValueAccessor, FormControl, FormsModule, NG_VALUE_ACCESSOR, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'shared-input',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule],
  templateUrl: './shared-input.component.html',
  styleUrl: './shared-input.component.css',
  providers: [{
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef(() => SharedInputComponent),
    multi: true
  }
  ]
})
export class SharedInputComponent implements ControlValueAccessor {
  placeholderText = input<string>('');
  inputClass = input<string>('');
  iconOnly = input<boolean>(false);
  addIcon = input<boolean>(false);
  iconClass = input<string>('');
  leftIcon = input<boolean>(false);
  inputType = input<string>('text');
  defaultValue = input<string>('');
  onValueChange = output<any>();
  inputChecked = input<boolean>(false);

  public value: string | boolean = '';
  public isDisabled: boolean = false;

  public onTouched: any = () => { };
  public isCheckbox: boolean = false;


  ngOnInit() {
    this.isCheckboxInput();
    this.value = this.defaultValue();
  }

  public isCheckboxInput(): void {
    this.isCheckbox = this.inputType() === 'checkbox';
  }

  writeValue(val: any) {
    if (this.isCheckbox) {
      this.value = !!val;
      return;
    }
    this.value = val ?? '';
  }

  registerOnChange(fn: any): void {
    this.onValueChange.subscribe(fn);
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
    this.isDisabled = isDisabled;
  }

  public onInputChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.value = this.isCheckbox ? target.checked : target.value;

    this.onValueChange.emit(this.value);
  }
}
