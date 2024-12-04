import * as React from "react";
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover_card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import withClickable from "@/lib/withClickable";

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string;
  skillName: string;
  description: string;
  damage?: number;
  accuracy?: number;
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, damage, accuracy, className, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            uid={`${uid}-button`}
            ref={ref}
            className={cn("w-full", className)}
            {...props}
          >
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            {(damage !== undefined || accuracy !== undefined) && (
              <div className="text-sm">
                {damage !== undefined && <div>Damage: {damage}</div>}
                {accuracy !== undefined && <div>Accuracy: {accuracy}%</div>}
              </div>
            )}
          </div>
        </HoverCardContent>
      </HoverCard>
    );
  }
);

SkillButton.displayName = "SkillButton";

SkillButton = withClickable(SkillButton);

export { SkillButton };
