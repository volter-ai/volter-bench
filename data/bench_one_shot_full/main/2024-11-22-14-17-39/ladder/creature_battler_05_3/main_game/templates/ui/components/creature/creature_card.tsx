import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui"
import { Progress } from "@/components/ui"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card 
        ref={ref} 
        className={cn("w-[350px]", className)} 
        uid={`${uid}-card`}
        {...props}
      >
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={image}
            alt={name}
            className="w-full h-48 object-contain mb-4"
          />
          <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          <div className="text-sm text-right mt-1">
            {currentHp}/{maxHp} HP
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
