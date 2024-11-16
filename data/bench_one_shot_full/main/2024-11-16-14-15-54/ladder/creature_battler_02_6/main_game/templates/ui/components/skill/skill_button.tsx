import * as React from "react"
import { Button } from "@/components/ui/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { withClickable } from "@/lib/withClickable"
import { type ButtonProps } from "@/components/ui/button"

interface SkillButtonProps extends ButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  onClick?: () => void
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, damage, accuracy, onClick, ...props }, ref) => {
    return (
      <HoverCard uid={uid + "-hover"}>
        <HoverCardTrigger uid={uid + "-trigger"} asChild>
          <Button
            ref={ref}
            uid={uid + "-button"}
            onClick={onClick}
            variant="outline"
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid + "-content"}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
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
