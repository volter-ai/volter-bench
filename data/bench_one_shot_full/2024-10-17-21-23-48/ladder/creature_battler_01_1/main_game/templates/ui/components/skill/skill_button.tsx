import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof Button> {
  uid: string;
  skillName: string;
  description: string;
  stats: string;
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, stats, ...props }, ref) => (
    <HoverCard uid={`${uid}-hover-card`}>
      <HoverCardTrigger asChild uid={`${uid}-trigger`}>
        <Button ref={ref} uid={`${uid}-button`} {...props}>
          {skillName}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent uid={`${uid}-content`}>
        <div>
          <h3 className="font-bold">{skillName}</h3>
          <p>{description}</p>
          <p className="text-sm text-muted-foreground">{stats}</p>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
