import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { 
  Card as BaseCard, 
  CardContent as BaseCardContent, 
  CardHeader as BaseCardHeader, 
  CardTitle as BaseCardTitle 
} from "@/components/ui/card"
import { Progress as BaseProgress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let Progress = React.forwardRef<HTMLDivElement, { uid: string } & React.ComponentProps<typeof BaseProgress>>(
  ({ uid, ...props }, ref) => <BaseProgress ref={ref} {...props} />
)

let Card = React.forwardRef<HTMLDivElement, { uid: string } & React.ComponentProps<typeof BaseCard>>(
  ({ uid, ...props }, ref) => <BaseCard ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, { uid: string } & React.ComponentProps<typeof BaseCardContent>>(
  ({ uid, ...props }, ref) => <BaseCardContent ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, { uid: string } & React.ComponentProps<typeof BaseCardHeader>>(
  ({ uid, ...props }, ref) => <BaseCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, { uid: string } & React.ComponentProps<typeof BaseCardTitle>>(
  ({ uid, ...props }, ref) => <BaseCardTitle ref={ref} {...props} />
)

Progress = withClickable(Progress)
Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`} className="flex flex-col gap-4">
          <img
            src={imageUrl}
            alt={name}
            className="h-48 w-48 object-contain mx-auto"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{`${currentHp}/${maxHp}`}</span>
            </div>
            <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
