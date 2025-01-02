import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"

import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Trigger> {
  uid: string;
  skillName: string;
  skillDescription: string;
  skillStats: string;
}

let SkillButton = ({ uid, skillName, skillDescription, skillStats, ...props }: SkillButtonProps) => (
  <HoverCardPrimitive.Root>
    <HoverCardPrimitive.Trigger {...props}>
      {skillName}
    </HoverCardPrimitive.Trigger>
    <HoverCardPrimitive.Content>
      <div className="text-sm">
        <strong>Description:</strong> {skillDescription}
      </div>
      <div className="text-sm">
        <strong>Stats:</strong> {skillStats}
      </div>
    </HoverCardPrimitive.Content>
  </HoverCardPrimitive.Root>
)

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
