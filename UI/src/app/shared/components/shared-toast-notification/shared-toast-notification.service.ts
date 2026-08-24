import { InputSignal, Service, signal, WritableSignal } from '@angular/core';
import { SharedToastNotificationInterface } from './shared-toast-notification';

@Service()
export class SharedToastNotificationService {
    private sharedToastNotificationSignal: WritableSignal<SharedToastNotificationInterface[]> = signal<SharedToastNotificationInterface[]>([]);

    public readonly sharedToastNotification$ = this.sharedToastNotificationSignal.asReadonly();

    showNotification(message: string, type: string, duration: number = 5000): void {
        const id = Date.now() + Math.random();
        const newNotification: SharedToastNotificationInterface = { id, message, type };
        this.sharedToastNotificationSignal.update(notifications => [...notifications, newNotification]);
        setTimeout(() => {
            this.dismiss(id);
        }, duration);
    }

    dismiss(id: number): void {
        this.sharedToastNotificationSignal.update(notification => notification.filter((t) => t.id !== id));
    }
}
