import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCard> {
  uid: string;
  skillName: string;
  skillDescription: string;
  skillStats: string;
}

let SkillButton = React.forwardRef<HTMLDivElement, SkillButtonProps>(
  ({ uid, skillName, skillDescription, skillStats, ...props }, ref) => (
    <HoverCard {...props} ref={ref}>
      <HoverCardTrigger asChild>
        <button className="skill-button">{skillName}</button>
      </HoverCardTrigger>
      <HoverCardContent>
        <div className="skill-tooltip">
          <h3>{skillName}</h3>
          <p>{skillDescription}</p>
          <p>{skillStats}</p>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
);

SkillButton.displayName = "SkillButton";

SkillButton = withClickable(SkillButton);

export { SkillButton };
