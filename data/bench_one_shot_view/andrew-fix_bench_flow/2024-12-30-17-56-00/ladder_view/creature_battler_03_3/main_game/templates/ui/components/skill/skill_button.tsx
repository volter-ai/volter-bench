import * as React from "react";
import * as HoverCardPrimitive from "@/components/ui/hover-card";
import { cn } from "@/lib/utils";
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Trigger> {
  uid: string;
  skillName: string;
  skillDescription: string;
  skillStats: string;
}

let SkillButton = ({ uid, skillName, skillDescription, skillStats, ...props }: SkillButtonProps) => (
  <HoverCard>
    <HoverCardTrigger {...props}>
      {skillName}
    </HoverCardTrigger>
    <HoverCardContent>
      <div className="font-bold">{skillName}</div>
      <div>{skillDescription}</div>
      <div className="text-sm text-muted">{skillStats}</div>
    </HoverCardContent>
  </HoverCard>
);

SkillButton = withClickable(SkillButton);

export { SkillButton };
