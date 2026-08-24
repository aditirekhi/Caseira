export interface UserCalendarPlanDetailsCreateUpdate {
    recipe_id: string;
    plan_date: Date;
}

export interface UserCalendarPlanDetailsRead {
    user_calendar_plan_details_id: string;
    recipe_id: string;
    plan_date: string;
    user_id: string;
    recipe_name: string;
}
