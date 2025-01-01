import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardTrigger> {
  uid: string;
  description: string;
  stats: string;
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, description, stats, ...props }, ref) => (
    <HoverCard>
      <HoverCardTrigger ref={ref} {...props} />
      <HoverCardContent>
        <div>
          <p>{description}</p>
          <p>{stats}</p>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
)

// Set display name
SkillButton.displayName = "SkillButton"

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
