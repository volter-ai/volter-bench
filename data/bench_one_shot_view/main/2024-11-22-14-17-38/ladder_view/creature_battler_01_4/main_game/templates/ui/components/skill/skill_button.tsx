import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  name: string
  description: string
  stats: string
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button ref={ref} uid={`${uid}-button`} {...props}>
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            <div className="text-sm text-muted-foreground">
              {stats}
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
