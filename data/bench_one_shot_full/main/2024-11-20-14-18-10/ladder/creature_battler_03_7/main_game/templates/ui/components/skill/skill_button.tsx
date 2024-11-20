import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  onClick?: () => void
}

let SkillButton = ({ uid, name, description, damage, accuracy, onClick, ...props }: SkillButtonProps) => {
  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Button
          onClick={onClick}
          variant="outline"
          className="w-full"
          uid={uid}
          {...props}
        >
          {name}
        </Button>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="space-y-2">
          <h4 className="font-medium">{name}</h4>
          <p className="text-sm text-muted-foreground">{description}</p>
          {damage && <p className="text-sm">Damage: {damage}</p>}
          {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}

SkillButton.displayName = "SkillButton"

export { SkillButton }
