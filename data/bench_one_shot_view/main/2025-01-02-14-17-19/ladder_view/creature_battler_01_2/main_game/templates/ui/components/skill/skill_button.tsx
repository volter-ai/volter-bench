import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"

import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string;
  description: string;
  stats: string;
}

let SkillButton = ({ uid, description, stats, ...props }: SkillButtonProps) => {
  return (
    <HoverCardPrimitive.Root {...props}>
      <HoverCardPrimitive.Trigger asChild>
        <button className="skill-button">Skill</button>
      </HoverCardPrimitive.Trigger>
      <HoverCardPrimitive.Content>
        <div className="skill-tooltip">
          <p>{description}</p>
          <p>{stats}</p>
        </div>
      </HoverCardPrimitive.Content>
    </HoverCardPrimitive.Root>
  );
};

// Apply withClickable
SkillButton = withClickable(SkillButton);

export { SkillButton }
