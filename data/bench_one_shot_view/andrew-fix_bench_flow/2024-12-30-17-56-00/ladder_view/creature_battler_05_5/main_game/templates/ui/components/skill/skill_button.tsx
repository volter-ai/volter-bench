import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable.tsx"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardTrigger> {
  uid: string;
  description: string;
  stats: string;
}

let SkillButton = ({ uid, description, stats, ...props }: SkillButtonProps) => (
  <HoverCard>
    <HoverCardTrigger {...props} />
    <HoverCardContent>
      <div>
        <p>{description}</p>
        <p>{stats}</p>
      </div>
    </HoverCardContent>
  </HoverCard>
)

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
