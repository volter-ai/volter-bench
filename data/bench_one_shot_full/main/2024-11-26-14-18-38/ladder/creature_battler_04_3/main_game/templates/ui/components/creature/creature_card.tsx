import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardContent as ShadcnCardContent,
  CardFooter as ShadcnCardFooter,
  CardHeader as ShadcnCardHeader,
  CardTitle as ShadcnCardTitle,
} from "@/components/ui/card"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let Card = withClickable(ShadcnCard)
let CardContent = withClickable(ShadcnCardContent)
let CardFooter = withClickable(ShadcnCardFooter)
let CardHeader = withClickable(ShadcnCardHeader)
let CardTitle = withClickable(ShadcnCardTitle)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain"
          />
        </CardContent>
        <CardFooter uid={`${uid}-footer`}>
          <div className="w-full">
            <div className="flex justify-between mb-1">
              <span>HP</span>
              <span>{`${currentHp}/${maxHp}`}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-green-600 h-2.5 rounded-full"
                style={{ width: `${(currentHp / maxHp) * 100}%` }}
              />
            </div>
          </div>
        </CardFooter>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
