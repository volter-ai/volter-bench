import * as React from "react"
import { cn } from "@/lib/utils"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
  isPlayer?: boolean
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, isPlayer, ...props }, ref) => {
    return (
      <Card
        ref={ref}
        className={cn("w-[300px]", className)}
        uid={`${uid}-card`}
        {...props}
      >
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`} className="flex flex-col gap-4">
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{currentHp}/{maxHp}</span>
            </div>
            <Progress uid={`${uid}-hp-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </CardContent>
        <CardFooter uid={`${uid}-footer`}>
          <div className="text-sm text-muted-foreground">
            {isPlayer ? "Your Creature" : "Opponent's Creature"}
          </div>
        </CardFooter>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
