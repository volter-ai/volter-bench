import * as React from "react"
import { Button } from "@/components/ui/button/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card/hover_card"
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
  ({ uid, skillName, description, damage, accuracy, type, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid} asChild>
          <Button ref={ref} uid={uid} {...props}>
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm">{description}</p>
            <div className="text-sm">
              {damage && <div>Damage: {damage}</div>}
              {accuracy && <div>Accuracy: {accuracy}%</div>}
              {type && <div>Type: {type}</div>}
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
