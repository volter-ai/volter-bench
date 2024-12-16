import * as React from "react"
import { Button } from "@/components/ui/game/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/game/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof Button> {
  uid: string
  skillName: string
  description: string
  damage?: number
  accuracy?: number
  type?: string
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, damage, accuracy, type, className, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid} asChild>
          <Button uid={uid} ref={ref} {...props}>
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid}>
          <div className="space-y-2">
            <h4 className="font-medium leading-none">{skillName}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            {damage && <p className="text-sm">Damage: {damage}</p>}
            {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
            {type && <p className="text-sm">Type: {type}</p>}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
