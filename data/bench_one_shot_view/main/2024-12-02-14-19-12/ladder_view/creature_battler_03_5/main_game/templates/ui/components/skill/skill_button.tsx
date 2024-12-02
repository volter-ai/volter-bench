import * as React from "react"
import { Button } from "@/components/ui/button"
import { 
  HoverCard as ShadcnHoverCard, 
  HoverCardContent as ShadcnHoverCardContent, 
  HoverCardTrigger as ShadcnHoverCardTrigger 
} from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  skillName: string
  description: string
  damage?: number
  accuracy?: number
}

let HoverCard = ShadcnHoverCard
let HoverCardTrigger = ShadcnHoverCardTrigger
let HoverCardContent = ShadcnHoverCardContent

HoverCard = withClickable(HoverCard)
HoverCardTrigger = withClickable(HoverCardTrigger)
HoverCardContent = withClickable(HoverCardContent)

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, damage, accuracy, ...props }, ref) => {
    return (
      <HoverCard>
        <HoverCardTrigger asChild>
          <Button ref={ref} uid={uid} {...props}>
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm">{description}</p>
            {damage && <p className="text-sm">Damage: {damage}</p>}
            {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
