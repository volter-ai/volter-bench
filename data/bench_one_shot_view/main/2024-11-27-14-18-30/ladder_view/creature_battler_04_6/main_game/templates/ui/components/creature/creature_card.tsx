import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card } from "../card/card"
import { CardContent } from "../card/content"
import { CardHeader } from "../card/header"
import { CardTitle } from "../card/title"
import { Progress } from "../progress/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    const hpPercentage = (currentHp / maxHp) * 100

    return (
      <Card uid={`${uid}-card`} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="relative aspect-square w-full mb-4">
            <img
              src={imageUrl}
              alt={name}
              className="object-contain w-full h-full"
            />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{`${currentHp}/${maxHp}`}</span>
            </div>
            <Progress uid={`${uid}-progress`} value={hpPercentage} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
